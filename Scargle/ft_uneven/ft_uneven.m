  function data_out = ft_uneven( data_in )
% function data_out = ft_uneven( data_in )
%--------------------------------------------------------------------------
% Compute Fourier Transform of arbitrarily spaced data
% (Modified algorithm in ApJ 343, 1989, 874-887, Paper III)
% and the Lomb-Scargle periodogram 
%--------------------------------------------------------------------------
%  Input: data_in.xx_vec  -- Dependent variable samples
%         data_in.tt_vec  -- Corresponding sample times
%         data_in.ww_vec  -- Ealuate transform at these frequencies
%                            (radians per unit time)
%         data_in.wt_vec  -- Statistical weights (optional)
%         data_in.ft_sign -- Sign of the transform
%         data_in.tt_zero -- Origin of time
%--------------------------------------------------------------------------
% Output: data_out.ft_vec -- Fourier transform (complex)
%         data_out.ls_vec -- Lomb-Scargle periodogram (real)
%--------------------------------------------------------------------------

data_out = [];

 xx_vec = data_in.xx_vec;  
 tt_vec = data_in.tt_vec;  
 
 if isfield( data_in, 'wt_vec' )
     wt_vec = data_in.wt_vec;  
     do_wt = 1;
     xx_vec = wt_vec .* xx_vec;%do this part of the weigth once and for all
 else
     do_wt = 0;
 end

 ww_vec = data_in.ww_vec;  
ft_sign = data_in.ft_sign;
tt_zero = data_in.tt_zero;

num_xt = length( xx_vec );% number of samples
num_ww = length( ww_vec );% number of frequencies
if num_ww <= 0
    return
end
%------------------------------------------
%          Start Frequency Loop 
%------------------------------------------

cpu_0 = cputime;
for ii_ww = 1: num_ww
    
    wrun = ww_vec( ii_ww );

    if do_wt > 0 
                
        if wrun == 0

            ft_vec( ii_ww ) = sum( xx_vec ) / sqrt( num_xt );
            ls_vec( ii_ww ) = ft_vec( ii_ww ) .^2;

        else

            csum = sum( wt_vec .* cos( 2.0 * wrun * tt_vec ) );
            ssum = sum( wt_vec .* sin( 2.0 * wrun * tt_vec ) );
            wtau = 0.5 * atan2( ssum, csum );

            %---------------------------------
            %      Sum over the samples
            %---------------------------------

            sumr = sum( xx_vec .* cos( wrun * tt_vec - wtau ) );
            sumi = sum( xx_vec .* sin( wrun * tt_vec - wtau ) );

            scos2 = sum( wt_vec .* ( cos(  wrun * tt_vec - wtau ) ) .^ 2 );
            ssin2 = sum( wt_vec .* ( sin(  wrun * tt_vec - wtau ) ) .^ 2 );

            ft_real = sumr / ( sqrt(2) * sqrt( scos2 ) );
            ft_imag = ft_sign * sumi / ( sqrt(2) * sqrt( ssin2 ) );
            phi_this = wtau - wrun * tt_zero;

            ft_vec( ii_ww ) = complex( ft_real, ft_imag ) * exp( 1i * phi_this );

            % L-S periodogram 
            ls_vec( ii_ww ) = ( sumr .^2 / scos2 ) + ( sumi .^2 / ssin2 );

        end
         
    else
        
        if wrun == 0

            ft_vec( ii_ww ) = sum( xx_vec ) / sqrt( num_xt );
            ls_vec( ii_ww ) = ft_vec( ii_ww ) .^2;

        else

            csum = sum( cos( 2.0 * wrun * tt_vec ) );
            ssum = sum( sin( 2.0 * wrun * tt_vec ) );
            wtau = 0.5 * atan2( ssum, csum );

            %---------------------------------
            %      Sum over the samples
            %---------------------------------

            sumr = sum( xx_vec .* cos( wrun * tt_vec - wtau ) );
            sumi = sum( xx_vec .* sin( wrun * tt_vec - wtau ) );

            scos2 = sum( ( cos(  wrun * tt_vec - wtau ) ) .^ 2 );
            ssin2 = sum( ( sin(  wrun * tt_vec - wtau ) ) .^ 2 );

            ft_real = sumr / ( sqrt(2) * sqrt( scos2 ) );
            ft_imag = ft_sign * sumi / ( sqrt(2) * sqrt( ssin2 ) );
            phi_this = wtau - wrun * tt_zero;

            ft_vec( ii_ww ) = complex( ft_real, ft_imag ) * exp( 1i * phi_this );

            % L-S periodogram 
            ls_vec( ii_ww ) = ( sumr .^2 / scos2 ) + ( sumi .^2 / ssin2 );

        end
        
    end
    
   %print_progress( ii_ww, num_ww, 100, cpu_0 );
        
end

data_out.ft_vec = ft_vec;
data_out.ls_vec = ls_vec;
